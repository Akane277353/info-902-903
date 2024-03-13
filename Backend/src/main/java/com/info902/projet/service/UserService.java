package com.info902.projet.service;

import com.info902.projet.controller.request.AssociateAssistantRequest;
import com.info902.projet.controller.request.RegisterRequest;
import com.info902.projet.controller.response.UserResponse;
import com.info902.projet.model.Assistant;
import com.info902.projet.model.User;
import com.info902.projet.repository.AssistantRepository;
import com.info902.projet.repository.UserRepository;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Data
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private AssistantRepository assistantRepository;


    public UserResponse createUser(RegisterRequest registerRequest){

        Optional<User> user = userRepository.findByPseudo(registerRequest.getPseudo());

        if(user.isEmpty()){
            User newUser = User.builder()
                    .pseudo(registerRequest.getPseudo())
                    .password(registerRequest.getPassword())
                    .build();
            userRepository.save(newUser);

            UserResponse userResponse = new UserResponse(newUser.getId(), newUser.getPseudo());

            return userResponse;
        } else {
            return null;
        }

    }

    public UserResponse loginUser(RegisterRequest registerRequest){
        Optional<User> user = userRepository.findByPseudoAndPassword(registerRequest.getPseudo(), registerRequest.getPassword());
        if (user.isPresent()) {
            UserResponse userResponse = new UserResponse(user.get().getId(), user.get().getPseudo());
            return userResponse;
        } else {
            return null;
        }
    }

    public boolean associateAssistant(AssociateAssistantRequest associateAssistantRequest){
        User user = userRepository.findById(associateAssistantRequest.getIdUser()).orElseThrow();
        Optional<Assistant> assistant = assistantRepository.findByCode(associateAssistantRequest.getCode());
        var isPresent = false;
        if(assistant.isPresent()){
            if(assistant.get().getUser() == null) {
                assistant.get().setUser(user);
                user.getAssistants().add(assistant.get());
                userRepository.save(user);
                isPresent = true;
            }
        }
        return isPresent;



    }

}
