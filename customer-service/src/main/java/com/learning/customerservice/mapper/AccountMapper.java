package com.learning.customerservice.mapper;

import com.learning.customerservice.entity.AccountEntity;
import com.learning.customerservice.entity.CustomerEntity;
import com.learning.customerservice.model.AccountRequest;
import com.learning.customerservice.model.AccountResponse;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import java.util.List;

@Mapper(componentModel = "spring")
public interface AccountMapper {

    @Mapping(
            source = "customerEntity.id",
            target = "customerId"
    )
    AccountResponse entityToDto(AccountEntity accountEntity);

    @Mapping(
            source = "customerEntity.id",
            target = "customerId"
    )
    List<AccountResponse> toResponseList(List<AccountEntity> accountEntities);

}
