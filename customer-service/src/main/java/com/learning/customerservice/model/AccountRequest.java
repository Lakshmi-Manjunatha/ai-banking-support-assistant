package com.learning.customerservice.model;

import com.learning.customerservice.enums.AccountType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record AccountRequest( @NotNull
                              AccountType accountType,
                              @NotBlank
                              String currency) {
}
