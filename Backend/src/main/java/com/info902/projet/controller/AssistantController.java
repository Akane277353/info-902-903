package com.info902.projet.controller;

import com.info902.projet.controller.response.AssistantResponse;
import com.info902.projet.controller.response.ConfigResponse;
import com.info902.projet.model.Assistant;
import com.info902.projet.model.History;
import com.info902.projet.service.AssistantService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("assistant")
public class AssistantController {

    @Autowired
    private AssistantService assistantService;
    @GetMapping("/login")
    public Integer AssistantLogin(){
        return assistantService.createAssistant();
    }

    @GetMapping("/config/{code}")
    public ConfigResponse AssistantConfig(@PathVariable Integer code){
        return assistantService.getConfig(code);
    }

    @GetMapping("isvalid/{code}")
    public Boolean IsAssistantConfig(@PathVariable Integer code){
        return assistantService.isAssistantValid(code);
    }

    @GetMapping("{code}")
    public AssistantResponse GetAssistant(@PathVariable Integer code){
        return assistantService.getAssistant(code);
    }
}
