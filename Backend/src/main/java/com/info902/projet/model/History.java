package com.info902.projet.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@Entity
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "history")
public class History {

    @ManyToOne
    @JoinColumn(name = "assistant")
    private Assistant assistant;
    @Id
    @GeneratedValue
    private Long id;

    @Column(columnDefinition="TEXT")
    private String request;

    @Column(columnDefinition="TEXT")
    private String response;

    private Date date;



}
