# The agent selects Sources; the staged Course review is the human gate

_Narrowed by ADR-0005: there is no longer a staged-Course human review; the agent's review of the generated Course Definition is the quality gate on Source selection, and confirming the Course Research Request is the sole human gate._

Supersedes ADR-0001. The `create-course` workflow now takes a single source URL, and the agent researches the public web and selects the ordered free Sources itself, sized to the confirmed Course Duration. The one remaining content decision by a person is the Course Requester confirming the derived Course Research Request; the Course Reviewer's inspection of the hidden Moodle Course before packaging is the quality gate on the agent's Source selection. This trades the earlier explicit human selection step for a faster path, on the basis that the staged-Course review already forces a human to judge educational suitability before anything is packaged.
