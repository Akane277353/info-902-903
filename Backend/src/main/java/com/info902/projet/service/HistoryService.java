package com.info902.projet.service;

import com.info902.projet.controller.request.NewHistoryRequest;
import com.info902.projet.model.Assistant;
import com.info902.projet.model.History;
import com.info902.projet.repository.AssistantRepository;
import com.info902.projet.repository.HistoryRepository;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;

@Service
@Data
public class HistoryService {

    @Autowired
    private HistoryRepository historyRepository;

    @Autowired
    private AssistantRepository assistantRepository;

    public void createHistory(NewHistoryRequest newHistoryRequest){
        Assistant assistant = assistantRepository.findByCode(newHistoryRequest.getCode()).orElseThrow();
        History newHistory = History.builder().request(newHistoryRequest.getRequest()).response(newHistoryRequest.getResponse()).date(new Date()).assistant(assistant).build();
        assistant.getHistories().add(newHistory);
        historyRepository.save(newHistory);



    }

}
