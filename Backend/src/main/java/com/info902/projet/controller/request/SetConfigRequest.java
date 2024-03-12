package com.info902.projet.controller.request;

import lombok.Data;

@Data
public class SetConfigRequest {

    private Integer code;

    private String language;

    private String voice;

    private String wifiSSID;

    private String wifiPassword;

}
