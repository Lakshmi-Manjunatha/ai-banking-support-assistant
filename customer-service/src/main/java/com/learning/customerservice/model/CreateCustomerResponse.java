package com.learning.customerservice.model;

import java.time.LocalDateTime;

public record CreateCustomerResponse (Long id,
                                      LocalDateTime createdAt,
                                      LocalDateTime updatedAt) {
}
