# Prove Moodle delivery before automating Course design

_Narrowed by ADR-0005: clean Trial Restoration is no longer part of a course build; it is the on-demand `bin/course-package verify` path._

The workflow established Course Definition to Moodle generation, native backup, and clean trial restoration before connecting Course Brief generation. This staged technical gate keeps Moodle delivery failures separate from Course-design failures and remains the acceptance foundation for later changes to Course Brief inputs.
