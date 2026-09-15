package com.learning.customerservice.controller;

import com.learning.customerservice.model.CreateCustomerResponse;
import com.learning.customerservice.model.CustomerRequest;
import com.learning.customerservice.model.CustomerResponse;
import com.learning.customerservice.service.CustomerService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/customer")
public class CustomerController {

    private final CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    @PostMapping("/")
    public ResponseEntity<CreateCustomerResponse> createCustomer(@Valid @RequestBody CustomerRequest customer) {
        CreateCustomerResponse response = customerService.createCustomer(customer);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<CustomerResponse> getCustomer(@RequestParam Long id) {
        CustomerResponse response = customerService.getCustomer(id);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
