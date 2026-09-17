package com.learning.transactionservice.mapper;

import com.learning.transactionservice.entity.TransactionEntity;
import com.learning.transactionservice.model.TransactionRequest;
import com.learning.transactionservice.model.TransactionResponse;
import org.mapstruct.Mapper;

import java.util.List;

@Mapper(componentModel = "spring")
public interface TransactionMapper {

    TransactionResponse entityToDto(TransactionEntity transactionEntity);
    List<TransactionResponse> entityToDto(List<TransactionEntity> transactionEntity);
    TransactionEntity dtoToEntity(TransactionRequest transactionRequest);

}
