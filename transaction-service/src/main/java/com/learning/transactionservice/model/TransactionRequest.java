package com.learning.transactionservice.model;

import com.learning.transactionservice.enums.TransactionType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;

public record TransactionRequest(

    @NotNull
    Long accountId,
    @NotNull
    TransactionType transactionType,
    @NotNull
    BigDecimal amount,
    @NotBlank
    String currency,
    String description) {
}
