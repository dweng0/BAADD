import { BddDocument, FeatureData } from "../types.js";

export function generateBddContent(doc: BddDocument): string {
  const lines: string[] = [];

  lines.push("---");
  lines.push(`language: ${doc.frontmatter.language}`);
  lines.push(`framework: ${doc.frontmatter.framework}`);
  if (doc.frontmatter.build_cmd) {
    lines.push(`build_cmd: ${doc.frontmatter.build_cmd}`);
  }
  if (doc.frontmatter.test_cmd) {
    lines.push(`test_cmd: ${doc.frontmatter.test_cmd}`);
  }
  if (doc.frontmatter.lint_cmd) {
    lines.push(`lint_cmd: ${doc.frontmatter.lint_cmd}`);
  }
  if (doc.frontmatter.fmt_cmd) {
    lines.push(`fmt_cmd: ${doc.frontmatter.fmt_cmd}`);
  }
  lines.push(`birth_date: ${doc.frontmatter.birth_date}`);
  lines.push("---");

  if (doc.system_description) {
    lines.push("");
    lines.push(`System: ${doc.system_description}`);
  }

  for (const feature of doc.features) {
    lines.push(...generateFeatureLines(feature));
  }

  return lines.join("\n") + "\n";
}

function generateFeatureLines(feature: FeatureData): string[] {
  const lines: string[] = [];

  lines.push("");
  lines.push(`    Feature: ${feature.name}`);

  if (feature.background) {
    lines.push("");
    lines.push(`        Background:`);
    lines.push(`            Given ${feature.background.given}`);
  }

  for (const scenario of feature.scenarios) {
    lines.push("");
    lines.push(`        Scenario: ${scenario.name}`);
    lines.push(`            Given ${scenario.given}`);
    lines.push(`            When ${scenario.when}`);
    lines.push(`            Then ${scenario.then}`);
  }

  return lines;
}
