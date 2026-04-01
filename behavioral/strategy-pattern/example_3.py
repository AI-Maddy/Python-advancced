"""Strategy Pattern — Example 3: Validation Strategies.

A form validator applies a pluggable validation strategy to user input.
Different strategies validate email addresses, phone numbers, or passwords.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Holds the outcome of a validation check."""
    valid: bool
    errors: list[str] = field(default_factory=list)


class ValidationStrategy(ABC):
    """Abstract validation strategy."""

    @abstractmethod
    def validate(self, value: str) -> ValidationResult:
        """Validate *value* and return a ``ValidationResult``."""


class EmailValidationStrategy(ValidationStrategy):
    """Validates that a string looks like an e-mail address."""

    _PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def validate(self, value: str) -> ValidationResult:
        if self._PATTERN.match(value):
            return ValidationResult(valid=True)
        return ValidationResult(valid=False, errors=["Invalid email format"])


class PhoneValidationStrategy(ValidationStrategy):
    """Validates a US-style phone number (digits, dashes, spaces OK)."""

    _PATTERN = re.compile(r"^\+?1?\s?[\(\-]?\d{3}[\)\-\s]?\s?\d{3}[\-\s]?\d{4}$")

    def validate(self, value: str) -> ValidationResult:
        if self._PATTERN.match(value.strip()):
            return ValidationResult(valid=True)
        return ValidationResult(valid=False, errors=["Invalid phone number"])


class PasswordValidationStrategy(ValidationStrategy):
    """Validates password strength (length, uppercase, digit, special char)."""

    def validate(self, value: str) -> ValidationResult:
        errors: list[str] = []
        if len(value) < 8:
            errors.append("Must be at least 8 characters")
        if not any(c.isupper() for c in value):
            errors.append("Must contain an uppercase letter")
        if not any(c.isdigit() for c in value):
            errors.append("Must contain a digit")
        if not any(c in "!@#$%^&*" for c in value):
            errors.append("Must contain a special character (!@#$%^&*)")
        return ValidationResult(valid=not errors, errors=errors)


@dataclass
class FormField:
    """A form field that validates its value using a pluggable strategy."""
    name: str
    strategy: ValidationStrategy

    def validate(self, value: str) -> ValidationResult:
        result = self.strategy.validate(value)
        status = "OK" if result.valid else f"FAIL: {'; '.join(result.errors)}"
        print(f"  [{self.name}] '{value}' → {status}")
        return result


def main() -> None:
    email_field = FormField("email", EmailValidationStrategy())
    phone_field = FormField("phone", PhoneValidationStrategy())
    pwd_field = FormField("password", PasswordValidationStrategy())

    print("=== Email validation ===")
    email_field.validate("user@example.com")
    email_field.validate("not-an-email")

    print("\n=== Phone validation ===")
    phone_field.validate("555-867-5309")
    phone_field.validate("12345")

    print("\n=== Password validation ===")
    pwd_field.validate("Secure@1")
    pwd_field.validate("weak")
    pwd_field.validate("NoSpecial1")


if __name__ == "__main__":
    main()
