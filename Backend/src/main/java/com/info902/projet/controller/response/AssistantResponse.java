package com.info902.projet.controller.response;

import com.info902.projet.model.History;
import com.info902.projet.model.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.hibernate.annotations.GenericGenerator;
import org.hibernate.annotations.Parameter;

import java.util.ArrayList;
import java.util.List;

@Data
@AllArgsConstructor
public class AssistantResponse {


    private Integer code;

    private String language;

    private String voice;

    private String wifiSSID;

    private String wifiPassword;

    private List<HistoryResponse> histories = new ArrayList<>();

}
