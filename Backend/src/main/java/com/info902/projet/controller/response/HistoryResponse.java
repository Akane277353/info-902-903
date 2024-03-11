package com.info902.projet.controller.response;

import com.info902.projet.model.Assistant;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Date;

@Data
@AllArgsConstructor
public class HistoryResponse {

    private String request;

    private String response;

    private Date date;
}
