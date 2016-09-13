TRUST_ANCHOR = "Trust Anchor"
SIGNER_IDENTIFIER = "Identifier"
SIGNER_VER_KEY = "Verification Key"

TARGET_IDENTIFIER = "Target"
TARGET_VER_KEY = "Target Verification Key"
TARGET_END_POINT = "Target endpoint"

LINK_NONCE = "Nonce"
LINK_STATUS = "Invitation status"
LINK_LAST_SYNCED = "Last Synced"
LINK_STATUS_ACCEPTED = "Accepted"

class LinkInvitation:

    def __init__(self, name, signerIdentifier, signerVerKey, trustAnchor,
                 targetIdentifier, targetEndPoint, linkNonce):
        self.name = name
        self.signerIdentifier = signerIdentifier

        self.trustAnchor = trustAnchor
        self.targetIdentifier = targetIdentifier
        self.targetEndPoint = targetEndPoint
        self.linkNonce = linkNonce

        self.signerVerKey = signerVerKey
        self.updateState(None, None, None)

    def updateState(self, targetVerKey, linkStatus, linkLastSynced):
        self.targetVerkey = targetVerKey
        self.linkStatus = linkStatus,
        self.linkLastSynced = linkLastSynced

    @staticmethod
    def getFromDict(name, values):
        signerIdentifier = values[SIGNER_IDENTIFIER]
        trustAnchor = values[TRUST_ANCHOR]
        targetIdentifier = values[TARGET_IDENTIFIER]
        linkNonce = values[LINK_NONCE]

        signerVerKey = values.get(SIGNER_VER_KEY, None)
        targetEndPoint = values.get(TARGET_END_POINT, None)

        targetVerKey = values.get(TARGET_VER_KEY, None)
        linkStatus = values.get(LINK_STATUS, None)
        linkLastSynced = values.get(LINK_LAST_SYNCED, None)

        li = LinkInvitation(name, signerIdentifier, signerVerKey, trustAnchor,
                              targetIdentifier, targetEndPoint, linkNonce)
        li.updateState(targetVerKey, linkStatus, linkLastSynced)
        return li

    def getDictToBeStored(self) -> dict:
        fixed = {
            SIGNER_IDENTIFIER: self.signerIdentifier,
            TRUST_ANCHOR: self.trustAnchor,
            TARGET_IDENTIFIER: self.targetIdentifier,
            LINK_NONCE: self.linkNonce

        }
        optional = {}
        if self.signerVerKey:
            optional[SIGNER_VER_KEY] = self.signerVerKey
        if self.targetVerkey:
            optional[TARGET_VER_KEY] = self.targetVerkey
        if self.targetEndPoint:
            optional[TARGET_END_POINT] = self.targetEndPoint
        if self.linkStatus:
            optional[LINK_STATUS] = self.linkStatus
        if self.linkLastSynced:
            optional[LINK_LAST_SYNCED] = self.linkLastSynced

        fixed.update(optional)
        return fixed

    def getLinkInfo(self) -> str:
        trustAnchorStatus = '(not yet written to Sovrin)'
        targetVerKey = '<unknown, waiting for sync>'
        linkStatus = 'not verified, target verkey unknown'
        linkLastSynced = '<this link has not yet been synchronized>'

        if not self.linkStatus and self.linkStatus == LINK_STATUS_ACCEPTED:
            trustAnchorStatus = '(confirmed)'
            targetVerKey = '<same as target>'
            linkLastSynced = self.linkLastSynced
            linkStatus = self.linkStatus

        verKey = '<same as local identifier>'
        if self.signerVerKey:
            verKey = self.signerVerKey

        info = \
            '\n' \
            'Name: ' + self.name + '\n' \
            'Identifier: ' + self.signerIdentifier + '\n' \
            'Trust anchor: ' + self.trustAnchor + ' ' + trustAnchorStatus + '\n' \
            'Verification key: ' + verKey + '\n' \
            'Signing key: <hidden>' '\n' \
            'Target: ' + self.targetIdentifier + '\n' \
            'Target Verification key: ' + targetVerKey + '\n' \
            'Target endpoint: ' + self.targetEndPoint + '\n' \
            'Invitation nonce: ' + self.linkNonce + '\n' \
            'Invitation status: ' + linkStatus + '\n' \
            'Last synced: ' + linkLastSynced + '\n'

        return info