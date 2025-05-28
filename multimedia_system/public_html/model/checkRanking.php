<?php

// Función que obtiene el top 10 de usuarios con mejor puntuación.
// Realiza una consulta que ordena a los usuarios por su score en forma descendente y limita a 10 resultados.
// Devuelve un array con nombre, email y puntuación de esos usuarios.
function getTopRanking($connection) {
    $sql_top = "SELECT name, email, score FROM \"user\" ORDER BY score DESC LIMIT 10";
    $query_top = pg_query($connection, $sql_top) or die("Error al ejecutar la consulta del ranking top 10");
    $result_top = pg_fetch_all($query_top);
    return $result_top;
}

// Función que obtiene la posición en el ranking y los datos de un usuario específico.
// Utiliza una subconsulta con ROW_NUMBER para asignar posiciones según la puntuación,
// y luego filtra para devolver solo el usuario indicado por su id.
// Retorna un array asociativo con posición, nombre, email y puntuación.
function getUserRanking($connection, $id_user) {
    $sql_position = "
      SELECT position, name, email, score FROM (
        SELECT id_user, name, email, score,
               ROW_NUMBER() OVER (ORDER BY score DESC) AS position
        FROM \"user\"
      ) AS ranked
      WHERE id_user = $id_user
    ";
  
    $query_position = pg_query($connection, $sql_position) or die("Error al ejecutar la consulta de posición del usuario");
    $result_position = pg_fetch_assoc($query_position);
    return $result_position;
  }  

?>
