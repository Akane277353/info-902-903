package com.info902.projet.service;

import com.info902.projet.controller.response.AssistantResponse;
import com.info902.projet.controller.response.ConfigResponse;
import com.info902.projet.controller.response.HistoryResponse;
import com.info902.projet.model.Assistant;
import com.info902.projet.model.History;
import com.info902.projet.model.User;
import com.info902.projet.repository.AssistantRepository;
import com.info902.projet.repository.HistoryRepository;
import com.info902.projet.repository.UserRepository;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Data
@Service
public class AssistantService {

    @Autowired
    private AssistantRepository assistantRepository;

    @Autowired
    private HistoryRepository historyRepository;

    @Autowired
    private UserRepository userRepository;

    public Integer createAssistant(){
        Assistant newAssistant = Assistant.builder().language("fr").voice("basic").wifiPassword("").wifiSSID("").build();
        assistantRepository.save(newAssistant);
        return newAssistant.getCode();
    }

    public ConfigResponse getConfig(Integer code){
        var assistant = assistantRepository.findByCode(code).orElseThrow();
        ConfigResponse configResponse = new ConfigResponse(assistant.getLanguage(), assistant.getVoice(), assistant.getWifiSSID(), assistant.getWifiPassword());
        return configResponse;
    }

    public Boolean isAssistantValid(Integer code){
        Optional<Assistant> assistant = assistantRepository.findByCode(code);
        var valid = false;
        if(assistant.isPresent()){
            valid = true;
        }
        return valid;
    }

    public AssistantResponse getAssistant(Integer code){

        var assistant = assistantRepository.findByCode(code).orElseThrow();
        List<History> historyList = assistant.getHistories();
        List<HistoryResponse> historyResponseList = new ArrayList<>();

        for(int i=0; i<historyList.size(); i++ ){
            HistoryResponse historyResponse = new HistoryResponse(historyList.get(i).getRequest(), historyList.get(i).getResponse(), historyList.get(i).getDate() );
            historyResponseList.add(historyResponse);
        }

        AssistantResponse assistantResponse = new AssistantResponse(assistant.getCode(), assistant.getLanguage(), assistant.getVoice(), assistant.getWifiSSID(), assistant.getWifiPassword(), historyResponseList);
        return assistantResponse;
    }

    public List<AssistantResponse> getAssistantOfUser(Long id){
        var user = userRepository.findById(id).orElseThrow();
        var assistants = user.getAssistants();
        var listAssistant = new ArrayList<AssistantResponse>();
        for(int i = 0; i<assistants.size(); i++){
            listAssistant.add(getAssistant(assistants.get(i).getCode()));
        }
        return listAssistant;
    }

}
