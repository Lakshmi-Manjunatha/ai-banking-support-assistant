package com.learning.customerservice.repositories;

import com.learning.customerservice.entity.AccountEntity;
import com.learning.customerservice.enums.AccountStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface AccountRepository extends JpaRepository<AccountEntity, Long> {
    List<AccountEntity> findByCustomerEntityId(Long customerId);

    @Query(""" 
            Select a
            From AccountEntity a
            where a.customerEntity.id = :customerId
            and a.accountStatus = ACTIVE
            """)
    List<AccountEntity> findActiveAccountsByCustomer( @Param("customerId") Long customerId,
                                                                @Param("status") AccountStatus status);
}
