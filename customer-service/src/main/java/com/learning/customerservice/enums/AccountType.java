package com.learning.customerservice.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum AccountType {

    CURRENT(1),
    SAVINGS(2);

    private final int accountTypeCode;
}
