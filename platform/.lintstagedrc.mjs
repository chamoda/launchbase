import path from "path";

const buildEslintCommand = (filenames) =>
  `eslint --fix ${filenames
    .map((f) => path.relative(process.cwd(), f))
    .join(" ")}`;

const config = {
  // Run prettier first, then ESLint (which includes both general linting and Next.js rules)
  "*.{js,jsx,ts,tsx}": ["prettier --write", buildEslintCommand],

  // Format other files with prettier
  "*.{json,md,yaml,yml}": ["prettier --write"],

  // Format CSS files
  "*.{css,scss,sass}": ["prettier --write"],
};

export default config;
