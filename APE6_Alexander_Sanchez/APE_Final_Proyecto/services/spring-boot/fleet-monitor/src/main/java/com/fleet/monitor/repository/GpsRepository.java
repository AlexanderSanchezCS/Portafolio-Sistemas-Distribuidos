package com.fleet.monitor.repository;

import com.fleet.monitor.model.GpsEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GpsRepository extends JpaRepository<GpsEntity, Long> {

    @Query("SELECT COUNT(DISTINCT g.vehicleId) FROM GpsEntity g")
    long countDistinctVehicleId();

    List<GpsEntity> findTop10ByVehicleIdOrderByIdDesc(String vehicleId);
}
