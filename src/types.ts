export type Step =
  | "language"
  | "framework"
  | "build_cmd"
  | "test_cmd"
  | "lint_cmd"
  | "fmt_cmd"
  | "system_description"
  | "feature_or_done"
  | "feature_name"
  | "feature_action"
  | "scenario_name"
  | "scenario_given"
  | "scenario_when"
  | "scenario_then"
  | "background_given"
  | "complete";

export type ScenarioData = {
  name: string;
  given: string;
  when: string;
  then: string;
};

export type BackgroundData = {
  given: string;
};

export type FeatureData = {
  name: string;
  background: BackgroundData | null;
  scenarios: ScenarioData[];
};

export type Frontmatter = {
  language: string;
  framework: string;
  build_cmd: string;
  test_cmd: string;
  lint_cmd: string;
  fmt_cmd: string;
  birth_date: string;
};

export type BddDocument = {
  frontmatter: Frontmatter;
  system_description: string;
  features: FeatureData[];
};
