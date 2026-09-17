package com.learning.customerservice.service;

import com.learning.customerservice.entity.AccountEntity;
import com.learning.customerservice.entity.CustomerEntity;
import com.learning.customerservice.enums.AccountStatus;
import com.learning.customerservice.exception.AccountNotFoundException;
import com.learning.customerservice.exception.CustomerNotFoundException;
import com.learning.customerservice.mapper.AccountMapper;
import com.learning.customerservice.model.AccountRequest;
import com.learning.customerservice.model.AccountResponse;
import com.learning.customerservice.repositories.AccountRepository;
import com.learning.customerservice.repositories.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

@Service
@RequiredArgsConstructor
public class AccountService {
    private final AccountMapper accountMapper;
    private final AccountRepository accountRepository;
    private final CustomerRepository customerRepository;

    public AccountResponse createAccount(Long customerId, AccountRequest accountRequest) {

        CustomerEntity customerEntity = customerRepository.findById(customerId)
                .orElseThrow(() -> new CustomerNotFoundException("Customer not found, verify given customer id"));

        AccountEntity accountEntity = new AccountEntity();
        accountEntity.setCustomerEntity(customerEntity);
        accountEntity.setAccountNumber(generateAccountNumber());
        accountEntity.setAccountType(accountRequest.accountType());
        accountEntity.setCurrency(accountRequest.currency());
        accountEntity.setAccountStatus(AccountStatus.ACTIVE);
        accountEntity.setBalance(BigDecimal.ZERO);
        accountEntity.setDailyTransferLimit(new BigDecimal("5000.00"));

        accountEntity = accountRepository.save(accountEntity);
        return accountMapper.entityToDto(accountEntity);
    }

    public AccountResponse getAccount(Long accountId) {
        AccountEntity accountEntity = accountRepository.findById(accountId)
                .orElseThrow(() -> new AccountNotFoundException("Account not found, check your ID"));
        return accountMapper.entityToDto(accountEntity);
    }

    public List<AccountResponse> getAccountsByCustomer(Long customerId) {
        List<AccountEntity> accountEntities = accountRepository.findByCustomerEntityId(customerId);

        if (accountEntities.isEmpty()) {
            throw new CustomerNotFoundException("Given Customer Id does not have any active accounts");
        }

        return accountMapper.toResponseList(accountEntities);
    }

    public List<AccountResponse> getActiveAccountsByCustomer(Long customerId) {
        List<AccountEntity> accountEntities = accountRepository.
                findActiveAccountsByCustomer(customerId, AccountStatus.ACTIVE);

        if (accountEntities.isEmpty()) {
            throw new CustomerNotFoundException("Given Customer Id does not have any active accounts");
        }
        
        return accountMapper.toResponseList(accountEntities);
    }

    private String generateAccountNumber() {
        long number = ThreadLocalRandom.current()
                .nextLong(10_000_000L, 100_000_000L);

        return String.valueOf(number);
    }
}
