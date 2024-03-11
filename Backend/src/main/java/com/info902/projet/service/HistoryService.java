package com.info902.projet.service;

import com.info902.projet.controller.request.NewHistoryRequest;
import com.info902.projet.model.Assistant;
import com.info902.projet.model.History;
import com.info902.projet.repository.AssistantRepository;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;

@Service
@Data
public class HistoryService {



    @Autowired
    private AssistantRepository assistantRepository;

    public void createHistory(NewHistoryRequest newHistoryRequest){
        Assistant assistant = assistantRepository.findByCode(newHistoryRequest.getCode()).orElseThrow();
        History newHistory = History.builder().request(newHistoryRequest.getRequest()).response(newHistoryRequest.getResponse()).assistant(assistant).date(new Date()).build();
        assistant.getHistories().add(newHistory);
        assistantRepository.save(assistant);

    }

}
