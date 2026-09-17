package com.learning.transactionservice.service;

import com.learning.transactionservice.entity.TransactionEntity;
import com.learning.transactionservice.enums.TransactionStatus;
import com.learning.transactionservice.exception.TransactionNotFoundException;
import com.learning.transactionservice.mapper.TransactionMapper;
import com.learning.transactionservice.model.TransactionRequest;
import com.learning.transactionservice.model.TransactionResponse;
import com.learning.transactionservice.repositories.TransactionRepository;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final TransactionMapper transactionMapper;

    public TransactionResponse getTransaction(Long transactionId) {
       TransactionEntity transactionEntity = transactionRepository.findById(transactionId)
               .orElseThrow(() -> new TransactionNotFoundException("Transaction not found"));
        return transactionMapper.entityToDto(transactionEntity);
    }

    public List<TransactionResponse> getTransactionsByAccount(Long accountId) {
        List<TransactionEntity> transactionEntities = transactionRepository.findTransactionEntityByAccountId(accountId);

       if(transactionEntities.isEmpty()) {
           throw new TransactionNotFoundException("No transaction for this account id "+ accountId);
       }

        return transactionMapper.entityToDto(transactionEntities);
    }

    public TransactionResponse createTransaction(@Valid TransactionRequest request) {
        TransactionEntity transactionEntity = transactionMapper.dtoToEntity(request);
        transactionEntity.setStatus(TransactionStatus.PENDING);
         transactionEntity = transactionRepository.save(transactionEntity);
        return transactionMapper.entityToDto(transactionEntity);
    }
}
