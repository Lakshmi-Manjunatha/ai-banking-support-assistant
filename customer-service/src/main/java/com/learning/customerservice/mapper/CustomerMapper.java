package com.learning.customerservice.mapper;

import com.learning.customerservice.entity.CustomerEntity;
import com.learning.customerservice.model.CustomerRequest;
import com.learning.customerservice.model.CustomerResponse;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface CustomerMapper {

    CustomerResponse entityToDto(CustomerEntity customerEntity);
    CustomerEntity dtoToEntity(CustomerRequest customerRequest);

}
