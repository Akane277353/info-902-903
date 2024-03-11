package com.info902.projet.controller;

import com.info902.projet.controller.request.AssociateAssistantRequest;
import com.info902.projet.controller.request.RegisterRequest;
import com.info902.projet.controller.response.UserResponse;
import com.info902.projet.model.User;
import com.info902.projet.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController()
@CrossOrigin(origins = "*")
@RequestMapping("user")
public class UserController {

    @Autowired
    private UserService userService;
    @PostMapping("/register")
    public ResponseEntity<UserResponse> Register(@RequestBody RegisterRequest registerRequest){
        return ResponseEntity.ok(userService.createUser(registerRequest));
    }

    @PostMapping("/login")
    public ResponseEntity<UserResponse> Login(@RequestBody RegisterRequest registerRequest){
        return ResponseEntity.ok(userService.loginUser(registerRequest));
    }

    @GetMapping("/hello")
    public String Hello(){
        return "Hello";
    }

    @PostMapping("/associate")
    public void Associate(@RequestBody AssociateAssistantRequest associateAssistantRequest){
        userService.associateAssistant(associateAssistantRequest);
    }
}
