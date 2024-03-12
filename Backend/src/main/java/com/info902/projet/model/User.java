package com.info902.projet.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "User")
public class User{

    @Id
    @GeneratedValue
    private Long id;

    private String pseudo;

    private String password;

    @OneToMany(mappedBy = "user")
    private List<Assistant> assistants = new ArrayList<>();

}
