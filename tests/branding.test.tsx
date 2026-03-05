import React from "react";
import { render } from "ink-testing-library";
import { describe, it, expect } from "vitest";
import App from "../src/app.js";

describe("Application branding", () => {
  describe("A sheep mascot is displayed when the application starts", () => {
    it("shows a sheep mascot in the terminal on startup", () => {
      const { lastFrame } = render(<App />);
      expect(lastFrame()).toContain("sheep");
    });
  });
});
