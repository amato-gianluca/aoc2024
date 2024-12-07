/**
 * A Java implementation of problems of Day 6 in order to compare performance with the Python ones.
 */
package puzzle6;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

record Vector2D(int i, int j) {

    Vector2D add(Vector2D other) {
        return new Vector2D(this.i + other.i, this.j + other.j);
    }

    Vector2D rotated() {
        return new Vector2D(this.j, -this.i);
    }
}


enum GuardResult {
    NORMAL, EXIT, LOOP
}


class Guard {
    final String[] map;
    final int numRows;
    final int numCols;
    final Vector2D startingPosition;
    final List<Vector2D>[][] visited;
    final List<Vector2D> obstacles;

    Vector2D direction;
    Vector2D position;

    Guard(String[] aMap) {
        map = aMap;
        numRows = map.length;
        numCols = map[0].length();
        startingPosition = startingPosition(aMap);
        visited = new ArrayList[numRows][numCols];
        for (int i = 0; i < visited.length; i++)
            for (int j = 0; j < visited[i].length; j++)
                visited[i][j] = new ArrayList<Vector2D>();
        obstacles = new ArrayList<Vector2D>();
        clear();
    }

    void clear() {
        position = startingPosition;
        direction = new Vector2D(-1, 0);
        for (int i = 0; i < visited.length; i++)
            for (int j = 0; j < visited[i].length; j++)
                visited[i][j].clear();
        visited[position.i()][position.j()].add(direction);
        obstacles.clear();
    }

    static Vector2D startingPosition(String[] map) {
        for (var i = 0; i < map.length; i++) {
            var j = map[i].indexOf('^');
            if (j > 0)
                return new Vector2D(i, j);
        }
        return new Vector2D(0, 0);
    }

    void addObstacle(Vector2D obs) {
        obstacles.add(obs);
    }

    GuardResult step() {
        var newPosition = position.add(direction);
        var i = newPosition.i();
        var j = newPosition.j();
        if (0 <= i && i < numRows && 0 <= j && j < numCols) {
            if (map[i].charAt(j) == '#' || obstacles.contains(newPosition)) {
                direction = direction.rotated();
                i = position.i();
                j = position.j();
            } else
                position = newPosition;
            if (visited[i][j].contains(direction))
                return GuardResult.LOOP;
            else {
                visited[i][j].add(direction);
                return GuardResult.NORMAL;
            }
        } else {
            return GuardResult.EXIT;
        }
    }

    int countVisited() {
        var count = 0;
        for (int i = 0; i < visited.length; i++)
            for (int j = 0; j < visited[i].length; j++)
                if (!visited[i][j].isEmpty())
                    count += 1;
        return count;
    }

    GuardResult run() {
        GuardResult ret;
        do {
            ret = step();
        } while (ret == GuardResult.NORMAL);
        return ret;
    }
}


public class All {

    static String[] readMap(String fileName) {
        List<String> lines;
        try {
            lines = Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new Error("Cannot read file");
        }
        var result = new String[lines.size()];
        lines.toArray(result);
        return result;
    }

    static boolean loopDetect(Guard g, Vector2D obs) {
        g.clear();
        g.addObstacle(obs);
        return g.run() == GuardResult.LOOP;
    }

    static int findLoops(Guard g) {
        var isVisited = new boolean[g.numRows][g.numCols];
        for (int i = 0; i < g.numRows; i++)
            for (int j = 0; j < g.numCols; j++)
                isVisited[i][j] = !g.visited[i][j].isEmpty();
        var numLoops = 0;
        for (int i = 0; i < g.numRows; i++) {
            for (int j = 0; j < g.numCols; j++) {
                var obstacle = new Vector2D(i, j);
                if (g.startingPosition != obstacle && isVisited[i][j] && loopDetect(g, obstacle))
                    numLoops += 1;
            }
        }
        return numLoops;
    }

    public static void main(String[] args) {
        Instant start = Instant.now();

        var mapData = readMap("puzzle6/input");
        var g = new Guard(mapData);
        g.run();
        System.out.println("part 1: " + g.countVisited());
        System.out.println("part 2: " + findLoops(g));
        Instant finish = Instant.now();
        long timeElapsed = Duration.between(start, finish).toMillis();
        System.out.println("--- " + timeElapsed / 1000.0 + " seconds ---");
    }
}
