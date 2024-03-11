package com.info902.projet.repository;

import com.info902.projet.model.History;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface HistoryRepository extends CrudRepository<History, Long> {

}
