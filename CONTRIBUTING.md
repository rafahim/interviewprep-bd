# Contributing to InterviewPrep BD

Thanks for helping keep interview preparation practical, accurate and accessible in Bengali and English.

## Ways to contribute

- Fix a bug or accessibility issue.
- Improve Bengali wording, examples, edge cases or time/space analysis.
- Add a complete interview question in the appropriate `content/` category.
- Improve search, mobile usability, progress tracking, flashcards or documentation.

## Question quality checklist

1. State a precise prompt and constraints.
2. Include a sample input/output and explain what it demonstrates.
3. Explain the approach in Bengali without skipping the important invariant.
4. For DSA, include correct Python and JavaScript solutions.
5. Check time and auxiliary-space complexity against the actual implementation.
6. Include empty, minimum, duplicate, invalid or boundary cases when relevant.
7. Add concise tags, valid related slugs, company/frequency metadata only when defensible, and a useful flashcard.
8. Keep answers original and do not copy proprietary interview material or personal candidate data.

## Run locally

```bash
npm install
npm run dev
npm run typecheck
npm run build
```

Open `http://localhost:3000/interview-prep/`. Run `npm run generate:sitemap` after adding or renaming content. The new slug should appear in `public/sitemap.xml` and render under `/interview-prep/questions/<slug>/`.

## MDX frontmatter

Use the template in the README. Add the file to the category directory matching its `category` value. Slugs must be unique and lowercase kebab-case. Related slugs must already exist or be added in the same pull request.

## Pull requests

Keep each PR focused. Explain what changed, why it matters, how it was tested and include screenshots for visible UI changes. Do not commit `.env`, keys, generated `.next/`, `node_modules/` or personal data. Review all modified files before requesting review.

## Reporting security issues

Do not post exploitable vulnerabilities or secrets in a public issue. Follow the private reporting instructions in `public/.well-known/security.txt`.
