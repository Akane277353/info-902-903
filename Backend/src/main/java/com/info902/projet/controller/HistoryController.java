package com.info902.projet.controller;

import com.info902.projet.controller.request.NewHistoryRequest;
import com.info902.projet.service.HistoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("history")
public class HistoryController {

    @Autowired
    private HistoryService historyService;

    @PostMapping("/new")
    public void NewHistory(@RequestBody NewHistoryRequest newHistoryRequest){
        historyService.createHistory(newHistoryRequest);
    }


}
