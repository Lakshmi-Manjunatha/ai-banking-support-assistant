package com.learning.customerservice.model;

import java.time.LocalDateTime;

public record CustomerResponse(Long id,
                               String firstName,
                               String lastName,
                               String email,
                               String accountType,
                               String status,
                               LocalDateTime createdAt,
                               LocalDateTime updatedAt) {
}
