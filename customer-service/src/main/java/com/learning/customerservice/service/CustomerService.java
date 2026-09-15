package com.learning.customerservice.service;

import com.learning.customerservice.entity.CustomerEntity;
import com.learning.customerservice.exception.CustomerNotFoundException;
import com.learning.customerservice.mapper.CustomerMapper;
import com.learning.customerservice.model.CreateCustomerResponse;
import com.learning.customerservice.model.CustomerRequest;
import com.learning.customerservice.model.CustomerResponse;
import com.learning.customerservice.repositories.CustomerRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class CustomerService {

    private final CustomerRepository customerRepository;
    private final CustomerMapper customerMapper;


    public CreateCustomerResponse createCustomer(CustomerRequest customerRequest) {

        CustomerEntity customerEntity = customerMapper.dtoToEntity(customerRequest);
        customerEntity = customerRepository.save(customerEntity);
        return new CreateCustomerResponse(customerEntity.getId(), customerEntity.getCreatedAt(), customerEntity.getUpdatedAt());
    }


    public CustomerResponse getCustomer(Long id) {
        CustomerEntity customerEntity =  customerRepository.findById(id)
                .orElseThrow(() -> new CustomerNotFoundException(id + " Customer Id not found"));
       return customerMapper.entityToDto(customerEntity);
    }
}
