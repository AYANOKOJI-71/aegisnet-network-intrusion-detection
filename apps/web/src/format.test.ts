import { describe, expect, it } from "vitest";
import { formatBytes, titleCase } from "./format";

describe("security operation formatters", () => {
  it("formats classifications and safe metadata values", () => {
    expect(titleCase("dns-exfiltration-signal")).toBe("Dns Exfiltration Signal");
    expect(formatBytes(2048)).toBe("2.0 KB");
  });
});
