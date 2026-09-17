package com.learning.customerservice.entity;


import com.learning.customerservice.enums.AccountStatus;
import com.learning.customerservice.enums.AccountType;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "accounts",uniqueConstraints = {@UniqueConstraint(
        name = "uk_account_number",
        columnNames = "account_number"
)})
@Data
public class AccountEntity {
    @Id
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "account_seq"
    )
    @SequenceGenerator(
            name = "account_seq",
            sequenceName = "account_id_seq",
            allocationSize = 50
    )
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "customer_id", referencedColumnName ="id", nullable = false)
    private CustomerEntity customerEntity;

    @Column(name = "account_number", nullable = false, unique = true, length = 8)
    private String accountNumber;

    private String sortCode = "09-06-20";

    @Column(name = "currency", nullable = false, length = 3)
    private String currency;

    @Enumerated(EnumType.STRING)
    @Column(name = "account_type", nullable = false)
    private AccountType accountType;


    @Enumerated(EnumType.STRING)
    @Column(name = "account_status", nullable = false)
    private AccountStatus accountStatus;

    @Column(name = "balance", nullable = false, precision = 19, scale = 2)
    private BigDecimal balance;


    @Column(name = "dailyTransferLimit", nullable = false, precision = 19, scale = 2)
    private BigDecimal dailyTransferLimit;

    @Column(name = "created_at", nullable = false, updatable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;

}
