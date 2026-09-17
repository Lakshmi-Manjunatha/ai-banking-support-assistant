package com.learning.customerservice.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum AccountStatus {

    ACTIVE(1),
    IN_ACTIVE(2);

    private final int statusCode;
}
