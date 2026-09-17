package com.learning.transactionservice.model;

import com.learning.transactionservice.enums.TransactionStatus;
import com.learning.transactionservice.enums.TransactionType;
import jakarta.validation.constraints.NotBlank;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record TransactionResponse(Long id,
                                  Long accountId,
                                  TransactionType transactionType,
                                  BigDecimal amount,
                                  String currency,
                                  String description,
                                  TransactionStatus status,
                                  String failureReason,
                                  LocalDateTime createdAt
) {}
