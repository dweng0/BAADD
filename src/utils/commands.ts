export type KnownCommands = {
  build_cmd: string;
  test_cmd: string;
  lint_cmd: string;
  fmt_cmd: string;
};

const LANGUAGE_DEFAULTS: Record<string, Partial<KnownCommands>> = {
  typescript: {
    build_cmd: "tsc",
    test_cmd: "npm test",
    lint_cmd: "eslint .",
    fmt_cmd: "prettier --write .",
  },
  javascript: {
    build_cmd: "npm run build",
    test_cmd: "npm test",
    lint_cmd: "eslint .",
    fmt_cmd: "prettier --write .",
  },
  python: {
    build_cmd: "python -m build",
    test_cmd: "pytest",
    lint_cmd: "flake8 .",
    fmt_cmd: "black .",
  },
  rust: {
    build_cmd: "cargo build",
    test_cmd: "cargo test",
    lint_cmd: "cargo clippy",
    fmt_cmd: "cargo fmt",
  },
  go: {
    build_cmd: "go build ./...",
    test_cmd: "go test ./...",
    lint_cmd: "golangci-lint run",
    fmt_cmd: "gofmt -w .",
  },
  java: {
    build_cmd: "mvn compile",
    test_cmd: "mvn test",
    lint_cmd: "mvn checkstyle:check",
    fmt_cmd: "mvn formatter:format",
  },
  ruby: {
    build_cmd: "bundle exec rake build",
    test_cmd: "bundle exec rspec",
    lint_cmd: "rubocop",
    fmt_cmd: "rubocop -a",
  },
};

export function inferCommand(
  language: string,
  commandType: keyof KnownCommands,
): string {
  const normalised = language.toLowerCase().trim();
  const defaults = LANGUAGE_DEFAULTS[normalised];
  if (defaults && defaults[commandType]) {
    return defaults[commandType] as string;
  }
  return `${commandType.replace("_cmd", "")}`;
}
