"""
Tests for Campaign Deletion.

These tests verify:
1. Deleting a paused/created/completed campaign succeeds and unlinks workflow runs
2. Attempting to delete a running campaign fails with 400 validation error
3. Deleting a non-existent campaign returns 404
"""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from fastapi import HTTPException


class TestDeleteCampaignEndpoint:
    """Tests for DELETE /api/v1/campaign/{campaign_id} route logic."""

    @pytest.mark.asyncio
    async def test_delete_campaign_success(self):
        """Deleting a non-running campaign should succeed."""
        from api.routes.campaign import delete_campaign

        mock_user = MagicMock()
        mock_user.selected_organization_id = 1

        mock_campaign = MagicMock()
        mock_campaign.id = 42
        mock_campaign.state = "paused"

        with patch("api.routes.campaign.db_client") as mock_db:
            mock_db.get_campaign = AsyncMock(return_value=mock_campaign)
            mock_db.delete_campaign = AsyncMock(return_value=True)

            res = await delete_campaign(campaign_id=42, user=mock_user)

            assert res["id"] == 42
            assert res["message"] == "Campaign deleted successfully"
            mock_db.delete_campaign.assert_called_once_with(42, 1)

    @pytest.mark.asyncio
    async def test_delete_running_campaign_fails(self):
        """Deleting a running campaign should raise HTTPException 400."""
        from api.routes.campaign import delete_campaign

        mock_user = MagicMock()
        mock_user.selected_organization_id = 1

        mock_campaign = MagicMock()
        mock_campaign.id = 42
        mock_campaign.state = "running"

        with patch("api.routes.campaign.db_client") as mock_db:
            mock_db.get_campaign = AsyncMock(return_value=mock_campaign)

            with pytest.raises(HTTPException) as exc_info:
                await delete_campaign(campaign_id=42, user=mock_user)

            assert exc_info.value.status_code == 400
            assert "Cannot delete a running campaign" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_delete_nonexistent_campaign_returns_404(self):
        """Deleting a campaign that does not exist should return 404."""
        from api.routes.campaign import delete_campaign

        mock_user = MagicMock()
        mock_user.selected_organization_id = 1

        with patch("api.routes.campaign.db_client") as mock_db:
            mock_db.get_campaign = AsyncMock(return_value=None)

            with pytest.raises(HTTPException) as exc_info:
                await delete_campaign(campaign_id=999, user=mock_user)

            assert exc_info.value.status_code == 404
            assert "Campaign not found" in exc_info.value.detail
