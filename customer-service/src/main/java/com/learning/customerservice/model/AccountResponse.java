package com.learning.customerservice.model;

import com.learning.customerservice.enums.AccountStatus;
import com.learning.customerservice.enums.AccountType;

import java.time.LocalDateTime;

public record AccountResponse(Long id,
                              Long customerId,
                              String accountNumber,
                              AccountType accountType,
                              String currency,
                              Double balance,
                              AccountStatus accountStatus,
                              Double dailyTransferLimit,
                              LocalDateTime createdAt
                              ) {
}
