import { sanitizeString } from "../sanitizeString";

describe("sanitizeString function", () => {
  test("removes special characters and converts to lowercase", () => {
    const input = "Hello! This is a String with Some Special Characters: @#$%^&*()";
    const expectedOutput = "hello this is a string with some special characters ";

    const output = sanitizeString(input);

    expect(output).toEqual(expectedOutput);
  });

  test("handles empty string", () => {
    const input = "";
    const expectedOutput = "";

    const output = sanitizeString(input);

    expect(output).toEqual(expectedOutput);
  });

  test("handles string with no special characters", () => {
    const input = "Hello World";
    const expectedOutput = "hello world";

    const output = sanitizeString(input);

    expect(output).toEqual(expectedOutput);
  });
});
