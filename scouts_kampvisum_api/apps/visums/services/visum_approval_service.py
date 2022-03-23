from apps.visums.models import CampVisumApproval


class CampVisumApprovalService:
    def create_approval(self, *args, **kwargs):
        approval = CampVisumApproval()

        approval.full_clean()
        approval.save()

        return approval
