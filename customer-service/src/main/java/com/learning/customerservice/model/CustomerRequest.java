package com.learning.customerservice.model;

import jakarta.validation.constraints.NotBlank;

import java.time.LocalDateTime;

public record CustomerRequest (

    @NotBlank
    String firstName,
    @NotBlank
    String lastName,
    @NotBlank
    String email,
    @NotBlank
    String password,
    String status,
    @NotBlank
    String accountType) {
}
