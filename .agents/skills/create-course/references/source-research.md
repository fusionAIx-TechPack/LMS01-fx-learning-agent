# Source research

Use this reference while turning the confirmed Course Research Request into the ordered Sources for a Course.

## Candidate standard

Search the current public web for Sources that match the confirmed Course Research Request, starting from the URL the Course Requester entered. Rank eligible Source Candidates by topical fit. Treat identifiable authorship or publishing, genuine educational substance, traceable provenance, and freedom from obvious search spam as a simple credibility gate. Prefer official or primary Sources when candidates have similar topical fit.

Keep only Sources available without payment. A free Source may require an ordinary account, but mark it `sign-in required` and prefer anonymous access. Exclude access that depends on a paid subscription or company licence.

For every candidate, verify and record:

- exact title and canonical HTTP URL;
- publisher and stable provider item identifier;
- supported Source type from the current Brief contract;
- Source language (`en-US`);
- realistic Source duration and total activity duration in whole minutes;
- free-access basis and a canonical evidence URL;
- current availability;
- the specific contribution to the intended learning outcome;
- the ordered topics it covers;
- a short semantic Learning Activity name within the current navigation limit.

Open the actual Source and access-evidence page. A search-result snippet is discovery evidence, not final evidence. Flag sign-in requirements, regional restrictions, prerequisites, stale versions, and promotional material.

## Candidate record

Record the eligible Source Candidates you researched in a table with title, activity name, contribution, covered topics, language, Source minutes, activity minutes, Source URL, access basis, and a separate free-access evidence URL. Identify overlap or coverage gaps.

Keep the set small: the primary Source plus only the further Sources the Course Overview and topics actually need. Do not pad with weak Sources.

## Source selection

Select the ordered subset of Sources to use yourself, sized to the confirmed Course Duration. State the combined activity duration and confirm it is within the Course Duration. There is no separate human selection step and no human review of the staged Moodle Course; your step-5 review of the generated Course Definition is the quality gate on this selection, so make it deliberate.

## Research artifact

Always create the Source Research Dossier from `templates/source-candidates.md` as `output/<course-slug>/source-candidates-<assessment-date>.md`. Use a new versioned filename rather than overwriting an existing dossier. Record links, evidence, assessment date, the candidates you researched, the Sources you selected and their order, and any exclusions beside the Course artifacts.

## Brief mapping

Map the selected evidence to the current example and parser rather than maintaining a parallel schema here:

- inspect `examples/copilot-studio-course-brief.json` for shape;
- inspect `course_research/cli.py` for accepted values and validation limits;
- inspect `course_research/source_validation.py` for availability and time-budget gates.

Validate the completed Brief with `bin/course-definition build`; do not treat a hand-written JSON parse check as contract validation.
