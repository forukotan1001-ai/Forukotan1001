from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.core.settings import settings
from app.db.models import User, Organization, OrganizationMember, OrganizationRole, Meeting, WebhookDeadLetter
import json
from datetime import datetime

router = APIRouter()


def _ensure_test_enabled(request: Request):
    header_key = request.headers.get('x-test-key')
    secret = settings.TEST_RESET_SECRET or None
    if not (settings.TESTING or (secret and header_key == secret)):
        raise HTTPException(status_code=403, detail='Test fixtures not enabled')


@router.post('/fixtures/meeting')
async def fixture_create_meeting(payload: dict, request: Request, db: AsyncSession = Depends(get_db)):
    _ensure_test_enabled(request)
    title = payload.get('title') or 'E2E Meeting'
    owner_email = payload.get('owner_email')
    org_id = payload.get('org_id')
    extra = payload.get('extra') or {}

    if not org_id:
        # try find org named 'E2E Org', create it if missing
        res = await db.execute(select(Organization).where(Organization.name == 'E2E Org'))
        org = res.scalar_one_or_none()
        if not org:
            org = Organization(name='E2E Org')
            db.add(org)
            await db.commit()
            await db.refresh(org)
        org_id = org.id

    # find or create owner user
    owner = None
    if owner_email:
        res = await db.execute(select(User).where(User.email == owner_email))
        owner = res.scalar_one_or_none()
    if not owner:
        # fall back to any org member
        res = await db.execute(select(OrganizationMember).where(OrganizationMember.org_id == org_id))
        mem = res.scalars().first()
        if mem:
            resu = await db.execute(select(User).where(User.id == mem.user_id))
            owner = resu.scalar_one_or_none()

    if not owner and owner_email:
        # create a simple user for the owner
        u = User(email=owner_email, hashed_password='x')
        db.add(u)
        await db.commit()
        await db.refresh(u)
        owner = u

    if not owner:
        raise HTTPException(status_code=400, detail='No user found or created to assign as meeting owner')

    # ensure organization membership for this owner
    res = await db.execute(select(OrganizationMember).where(OrganizationMember.org_id == org_id, OrganizationMember.user_id == owner.id))
    mem = res.scalar_one_or_none()
    if not mem:
        m = OrganizationMember(org_id=org_id, user_id=owner.id, role=OrganizationRole.OWNER)
        db.add(m)
        await db.commit()

    meeting = Meeting(title=title, owner_id=owner.id, org_id=org_id, extra=extra)
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    return { 'id': meeting.id, 'org_id': org_id, 'owner_email': owner.email }


@router.post('/fixtures/webhook-deadletter')
async def fixture_create_deadletter(payload: dict, request: Request, db: AsyncSession = Depends(get_db)):
    _ensure_test_enabled(request)
    org_id = payload.get('org_id')
    url = payload.get('url') or 'http://example.invalid/hook'
    pl = payload.get('payload') or {}
    fr = payload.get('failure_reason') or 'e2e failure'

    if not org_id:
        raise HTTPException(status_code=400, detail='org_id is required')

    from sqlalchemy.exc import OperationalError
    from sqlalchemy import text
    try:
        dl = WebhookDeadLetter(org_id=org_id, url=url, payload=pl, failure_reason=fr)
        db.add(dl)
        await db.commit()
        await db.refresh(dl)
        return { 'id': dl.id }
    except OperationalError as e:
        # Rollback previous failed transaction so we can perform a raw INSERT fallback
        await db.rollback()
        # Fallback for mismatched schema in simple test envs: insert minimal columns directly
        # This tolerates missing columns introduced by newer migrations (e.g., last_replay_at)
        await db.execute(text("""
            INSERT INTO webhook_dead_letters (org_id, url, payload, failure_reason, processed, replay_count, auto_replay, created_at)
            VALUES (:org_id, :url, :payload, :failure_reason, 0, 0, 0, :created_at)
        """), {"org_id": org_id, "url": url, "payload": json.dumps(pl), "failure_reason": fr, "created_at": datetime.utcnow().isoformat()})
        await db.commit()
        # fetch last inserted row for this org/url
        res = await db.execute(select(WebhookDeadLetter).where(WebhookDeadLetter.org_id == org_id, WebhookDeadLetter.url == url).order_by(WebhookDeadLetter.id.desc()).limit(1))
        dl2 = res.scalar_one_or_none()
        if not dl2:
            raise
        return { 'id': dl2.id }


@router.get('/fixtures/dlq/debug')
async def fixture_dlq_debug(request: Request, db: AsyncSession = Depends(get_db)):
    """Test-only debug endpoint: return latest DLQ bulk job + items for inspection"""
    _ensure_test_enabled(request)
    from app.db.models import BulkDLQJob, BulkDLQJobItem
    res = await db.execute(select(BulkDLQJob).order_by(BulkDLQJob.id.desc()).limit(1))
    job = res.scalar_one_or_none()
    if not job:
        return { 'job': None, 'items': [] }
    res_items = await db.execute(select(BulkDLQJobItem).where(BulkDLQJobItem.job_id == job.id))
    items = res_items.scalars().all()
    return {
        'job': {
            'id': job.id,
            'org_id': job.org_id,
            'status': job.status,
            'total_items': job.total_items,
            'params': job.params,
            'created_at': getattr(job, 'created_at', None)
        },
        'items': [
            {
                'id': i.id,
                'dead_letter_id': i.dead_letter_id,
                'status': i.status,
                'attempts': i.attempts,
                'last_error': i.last_error
            }
            for i in items
        ]
    }

@router.post('/fixtures/dlq/deterministic')
async def fixture_set_dlq_deterministic(payload: dict, request: Request):
    """Test-only endpoint to toggle deterministic DLQ processing mode.

    Requires TEST fixtures to be enabled (via TESTING or correct X-TEST-KEY header).
    Accepts payload: {"enabled": true|false}
    """
    _ensure_test_enabled(request)
    enabled = bool(payload.get('enabled', False))
    settings.DLQ_BULK_DETERMINISTIC = enabled
    return { 'deterministic': enabled }
