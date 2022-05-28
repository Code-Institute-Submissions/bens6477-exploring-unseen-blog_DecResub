/**
 * @jest-environment jsdom
 */

const addition = require("../setup_test");

describe("Calculator", () => {
    describe("Addition funtion", () => {
        test("should return 42 for 20 + 22", () => {
            expect(addition(20, 22)).toBe(42);
        });
        test("should return 73 for 42 + 31", () => {
            expect(addition(42, 31)).toBe(73);
        });
    });
});