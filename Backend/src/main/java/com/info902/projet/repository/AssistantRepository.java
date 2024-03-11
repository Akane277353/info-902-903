package com.info902.projet.repository;

import com.info902.projet.model.Assistant;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AssistantRepository extends CrudRepository<Assistant, Integer> {

    Optional<Assistant> findByCode(Integer code);
}
