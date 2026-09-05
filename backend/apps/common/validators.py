import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Same allowlist as frontend/src/shared/ui/validators.js (isLatinOnly) — keep
# the two in sync. Cyrillic/Armenian is expected in user-facing content, but
# technical fields (login, slugs, filenames, keys) must reject any non-Latin
# input, so an allowlist regex is used instead of a Cyrillic-specific blocklist.
TECHNICAL_IDENTIFIER_RE = re.compile(r"^[a-zA-Z0-9_.-]+$")


def validate_technical_identifier(value):
    if not TECHNICAL_IDENTIFIER_RE.match(value):
        raise ValidationError(
            _("Only Latin letters, digits, '_', '-' and '.' are allowed here."),
            code="non_latin_technical_field",
        )
