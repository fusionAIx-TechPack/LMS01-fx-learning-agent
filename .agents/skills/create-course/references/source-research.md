# Source research

Use this reference while turning a Course idea into candidates for human selection.

## Candidate standard

Search the current public web for Sources that match the approved Course Research Request. Rank eligible Source Candidates by topical fit. Treat identifiable authorship or publishing, genuine educational substance, traceable provenance, and freedom from obvious search spam as a simple credibility gate. Prefer official or primary Sources when candidates have similar topical fit.

Keep only Sources available without payment. A free Source may require an ordinary account, but mark it `sign-in required` and prefer anonymous access. Exclude access that depends on a paid subscription or company licence.

For every candidate, verify and record:

- exact title and canonical HTTP URL;
- publisher and stable provider item identifier;
- supported Source type from the current Brief contract;
- Source language (`en-US`);
- realistic Source duration and total Source Activity duration in whole minutes;
- free-access basis and a canonical evidence URL;
- current availability;
- the specific contribution to the intended learning outcome;
- the ordered topics it covers;
- a short semantic Learning Activity name within the current navigation limit.

Open the actual Source and access-evidence page. A search-result snippet is discovery evidence, not final evidence. Flag sign-in requirements, regional restrictions, prerequisites, stale versions, and promotional material.

## Candidate presentation

Present a compact shortlist of 5–10 eligible Source Candidates. Use a table with title, activity name, contribution, covered topics, language, Source minutes, activity minutes, Source URL, access basis, and a separate free-access evidence URL. State the combined activity duration and compare it with the Course budget. Identify overlap or coverage gaps.

When fewer than five eligible candidates exist, present the smaller trustworthy shortlist and explain the coverage gaps instead of padding it with weak Sources.

Recommend an ordered subset and label it as advisory.

## Research artifact

Always create the Source Research Dossier from `templates/source-candidates.md` as `output/<course-slug>/source-candidates-<assessment-date>.md`. Use a new versioned filename rather than overwriting an existing dossier. Record links, evidence, assessment date, recommendation, exclusions, and the final human selection beside the Course artifacts.

## Brief mapping

Map the selected evidence to the current example and parser rather than maintaining a parallel schema here:

- inspect `examples/copilot-studio-course-brief.json` for shape;
- inspect `course_research/cli.py` for accepted values and validation limits;
- inspect `course_research/source_validation.py` for availability and time-budget gates.

Validate the completed Brief with `bin/course-definition build`; do not treat a hand-written JSON parse check as contract validation.
